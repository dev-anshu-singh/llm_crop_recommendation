import pytest
from datetime import datetime
from unittest.mock import MagicMock

# Since the function is in 'logic.py', we import it.
# We also need to import the schema it depends on.
from llm.logic import generate_recommendation
from schemas.input_output_schema import UserInput

# Define the path to the modules we need to mock.
# This tells the mocker where to find the objects to replace.
CHAIN_PATH = "llm.logic.chain"
STATIC_DATA_PATH = "llm.logic"


def test_generate_recommendation(mocker):
    """
    Tests the generate_recommendation function to ensure it correctly
    prepares the input dictionary and invokes the LCEL chain.
    """
    # 1. Setup Mocks
    # Mock the entire 'chain' module that is imported into 'logic.py'.
    mock_chain = mocker.patch(CHAIN_PATH)

    # We create a mock object that has a 'full_chain.invoke' method.
    # We can control what this mock returns to test how our function handles it.
    mock_chain.full_chain.invoke.return_value = {"recommendation": "Mocked Crop"}

    # Mock the data loading functions imported into 'logic.py'.
    mocker.patch(f"{STATIC_DATA_PATH}.load_msp_data", return_value={"wheat": 2200})
    mocker.patch(f"{STATIC_DATA_PATH}.load_fertilizer_data", return_value={"N": 100})

    # 2. Prepare Test Data
    # Create a valid UserInput object, just like FastAPI would.
    user_input = UserInput(
        latitude=28.6139,
        longitude=77.2090,
        farm_plot_size=5.0,
        irrigation_type=["drip"],
        previous_crop="wheat",
        excluded_crops=["tobacco"]
    )

    # 3. Execute the Function Under Test
    result = generate_recommendation(user_input)

    # 4. Assert the Results
    # Assert that the chain's invoke method was called exactly once.
    mock_chain.full_chain.invoke.assert_called_once()

    # Retrieve the arguments that 'invoke' was called with.
    # `call_args[0]` is a tuple of positional arguments. We want the first one.
    invoke_args = mock_chain.full_chain.invoke.call_args[0][0]

    # Check that the function correctly modified the input dictionary.
    assert "date" in invoke_args
    assert invoke_args["date"] == datetime.now().strftime("%Y-%m-%d")
    assert invoke_args["fertilizer_recommendation"] == {"N": 100}
    assert invoke_args["msp_prices"] == {"wheat": 2200}

    # Check that the original user input data is still present.
    assert invoke_args["latitude"] == 28.6139
    assert invoke_args["previous_crop"] == "wheat"

    # Assert that the final result is what the mocked chain returned.
    assert result == {"recommendation": "Mocked Crop"}

    print("\n✅ test_generate_recommendation: PASSED")
    print(result)