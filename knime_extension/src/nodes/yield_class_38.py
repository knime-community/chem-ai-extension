import logging

import os
import pandas as pd
import knime.extension as knext

from categories import yield_category
from utils.yield_repo.constants import YieldModelWeights
from utils.yield_utils import predict_yield
from exceptions.fluoriclogppka_exceptions import InvalidSettingsException

LOGGER = logging.getLogger(__name__)

@knext.node(name="Yield class 38", node_type=knext.NodeType.LEARNER, icon_path="icons/chem_icon.png", category=yield_category)
@knext.input_port(name="Input SMILES Data", description="Table with SMILES in 'string' of 'SMI' format", port_type=knext.PortType.TABLE)
@knext.output_table(name="Output Data", description="Table with predicted yield values for class 38")
class Yield38:
    """Node for predicting yield for class 38 using molecules SMILES.
    """

    selected_REAGENTSMI1_col = knext.ColumnParameter(
        "REAGENT SMILES 1 column:",
        "Select the column containing REAGENT SMILES 1.",
        column_filter= lambda col: True,
        include_row_key=False,
        include_none_column=False,
    )

    selected_REAGENTSMI2_col = knext.ColumnParameter(
        "REAGENT SMILES 2 column:",
        "Select the column containing REAGENT SMILES 2.",
        column_filter= lambda col: True,
        include_row_key=False,
        include_none_column=False,
    )

    selected_PRODUCTSMI_col = knext.ColumnParameter(
        "PRODUCT SMILES column:",
        "Select the column containing PRODUCT SMILES.",
        column_filter= lambda col: True,
        include_row_key=False,
        include_none_column=False,
    )

    def __init__(self) -> None:
        print(__file__)
        self.model_weights = os.path.join(os.path.dirname(os.path.dirname(__file__)), YieldModelWeights.CLASS_38.value)

    def obtain_smiles_column_values(self,
                                    column_parameter: knext.ColumnParameter = None,
                                    column_name: str = ""):
        if column_parameter is None:
            LOGGER.error(f"No {column_name} column is selected.")
            raise InvalidSettingsException(f"Please specify a {column_name} column.")
        
        selected_column_type = str(self.input_pandas.dtypes[column_parameter])
        is_smiles_column = "smiles" in selected_column_type.lower()
        if not is_smiles_column:
            LOGGER.error(f"Invalid SMILES column.")
            raise ValueError(f"The input data type of {column_name} is {selected_column_type} instead of SMILES. Please type cast.")

        LOGGER.info(f"SMILES column name: {column_parameter}, selected column name: {column_parameter}")

        return self.input_pandas[column_parameter]
        


    def configure(self, configure_context, input_schema_1):
        
        input_schema_1 = input_schema_1.append(knext.Column(knext.double(), "Yield"))

        return input_schema_1
 
    def execute(self, exec_context, input_1):
        input_pandas = input_1.to_pandas()
        self.input_pandas = input_pandas

        self.reagent_smiles1_column_name = self.selected_REAGENTSMI1_col
        REAGENTSMI1_array = self.obtain_smiles_column_values(
            column_parameter=self.selected_REAGENTSMI1_col,
            column_name="REAGENTSMI1"
        )
        REAGENTSMI2_array = self.obtain_smiles_column_values(
            column_parameter=self.selected_REAGENTSMI2_col,
            column_name="REAGENTSMI2"
        )
        PRODUCTSMI_array = self.obtain_smiles_column_values(
            column_parameter=self.selected_PRODUCTSMI_col,
            column_name="PRODUCTSMI"
        )
        
        total_number_of_operations = len(PRODUCTSMI_array) * 2
        
        predicted_yields = []
        for index, _ in enumerate(PRODUCTSMI_array):
            reaction_name = f"{REAGENTSMI1_array[index]}, {REAGENTSMI2_array[index]}, {PRODUCTSMI_array[index]}"
            
            is_any_cell_empty = pd.isnull(REAGENTSMI1_array[index]) or pd.isnull(REAGENTSMI2_array[index]) or pd.isnull(PRODUCTSMI_array[index])
            if is_any_cell_empty:
                predicted_yield = None
                LOGGER.warning(f"One of the cells are empty.")
            else:
                try:
                    predicted_yield = predict_yield(
                        REAGENTSMI1=REAGENTSMI1_array[index],
                        REAGENTSMI2=REAGENTSMI2_array[index],
                        PRODUCTSMI=PRODUCTSMI_array[index],
                        model_weights=self.model_weights,
                        execution_context=exec_context,
                        index=index * 2,
                        total_number_of_operations=total_number_of_operations
                    )
                except Exception as e:
                    LOGGER.error(f"Error predicting yield for SMILES '{reaction_name}'")
                    raise ValueError(f"Inappropriate SMILES format: {reaction_name}")

            predicted_yields.append(predicted_yield)

        output_df = input_pandas.copy()
        output_df['Yield'] = predicted_yields
        
        return knext.Table.from_pandas(output_df)
