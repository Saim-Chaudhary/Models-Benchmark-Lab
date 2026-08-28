# cost.py
# Calculates the dollar cost of a single model call.

def calculate_cost(model_name, input_tokens, output_tokens, pricing_table):
    """
    Looks up pricing for this model and calculates actual cost.
    Returns None if we don't have pricing data for this model
    (better to show 'unknown' than guess wrong).
    pricing_table is built from user input in the UI — we never
    hardcode prices here, since they change and vary by provider.
    """

    if model_name not in pricing_table:
        return None

    price = pricing_table[model_name]

    input_cost = (input_tokens / 1_000_000) * price["input"]
    output_cost = (output_tokens / 1_000_000) * price["output"]

    return round(input_cost + output_cost, 6)