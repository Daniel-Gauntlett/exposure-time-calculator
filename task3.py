vega_m_vega = 0
alt_m_vega = 28

scale_factor = 10 ** ((vega_m_vega - alt_m_vega) / -2.5)
print(scale_factor)

# Scale in AB system by Vega's magnitude in the above formula, different at each wavelegnth.