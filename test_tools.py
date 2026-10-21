from tools import (calculate_delay_compensation,calculate_damage_compensation,calculate_lost_compensation)
result1 = calculate_delay_compensation(
    10000,
    "The shipment is urgent and delayed."
)
print("Delay Test:", result1)

result2 = calculate_damage_compensation(
    10000,
    "The package arrived broken."
)
print("Damage Test:", result2)

# Test 3: Lost shipment
result3 = calculate_lost_compensation(
    10000,
    "The shipment never arrived."
)
print("Lost Test:", result3)