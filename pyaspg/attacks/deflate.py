def deflation_attack(real_net_power, **kwargs):
    return real_net_power * kwargs.get("deflation_rate", 0.9)
