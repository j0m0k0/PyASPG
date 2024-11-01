from pyaspg.attacks import inflate, deflate

# define hybrid_attack function
# it should have a criteria to determine which prosumers to inflate and which to deflate
# if it is true, inflate the prosumers, otherwise deflate them
# default criteria is True (which means inflate)
def hybrid_attack(net_power, **kwargs):
    if kwargs.get("criteria", True):
        return inflate.inflation_attack(net_power, inflation_rate=kwargs.get("inflation_rate", 1.1))
    else:
        return deflate.deflation_attack(net_power, deflation_rate=kwargs.get("deflation_rate", 0.9))
