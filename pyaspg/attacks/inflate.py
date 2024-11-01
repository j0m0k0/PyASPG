def inflation_attack(real_net_power, **kwargs):
    return real_net_power * kwargs.get("inflation_rate", 1.1)
