import numpy as np

def damper_pos_from_static(static,load_adj=0):
    """Calculates damper position from static pressure
        
    Args:
        static (float): static pressure, [0.3, 2.5]
        load_adj (int, optional): adjustment for different load condition, Defaults to 0.

    Returns:
        float: damper posistion in ratio. Example: 1 means 100% open, 0.7 means 70% open
    """
    coef = np.array([-0.221,1.1788,-2.1134,1.6964])
    pos_damper = coef[0]*static**3 + coef[1]*static**2 + coef[2]*static + coef[3] + load_adj
    return pos_damper

def fan_speed_from_static(static,fan_adj=1):
    """Calculates the fan speed from static pressure

    Args:
        static (float): static pressure, [0.3, 2.5]
        fan_adj (int, optional): adjustment for different load condition. Defaults to 1.

    Returns:
        float: fan speed in ratio. Example: 1 means 100% max speed, 0.7 means 70% speed
    """
    coef = np.array([28.345,0.3412])
    fan_speed = coef[0]*static**coef[1]*fan_adj
    return fan_speed/60

def fan_power_from_speed(freq, hp=15, eff=0.9):
    """Calculates the fan power (kW) from fan speed ratio

    Args:
        freq (float): fan speed in ratio, [0,1]
        hp (int, optional): horsepower of the fan. Defaults to 15, can change to other reasonable values.
        eff (float, optional): fan nominal efficiency. Defaults to 0.9, can change to other reasonable values.

    Returns:
        float: fan power in kW
    """
    a = 1.0608; b = -0.1222; c = 0.0684; d = 0.0022
    Pratio = a*freq**3 + b*freq**2 + c*freq + d
    fan_power = Pratio*hp*0.7457/eff
    return fan_power

def valve_pos_from_Tsa_static(T_sa, static):
    """Calculates the chw valve position (0,1] from supply air temp.(F) and static pressure

    Args:
        T_sa (float): supply air temperature, [55, 70]
        static (float): static pressure, [0.3, 2.5]

    Returns:
        float: CHW valve position, [0,1]
    """
    a = 0.0008; b = -0.1217; c = 4.8238
    valve_adjust = - (static - 1.5)*0.2
    pos_valve = a*T_sa**2 + b*T_sa + c + valve_adjust
    if pos_valve > 1:
        pos_valve = 1
    return pos_valve

def pump_speed_from_Tsa_static(T_sa, static):
    """Calculates the chw pump speed from supply air temp. and static pressure

    Args:
        T_sa (float): supply air temperature, [55, 70]
        static (float): static pressure, [0.3, 2.5]

    Returns:
        float: pump speed, [0,1]
    """
    base_speed = 0.6
    base_threashold = 60
    adj_threashold = base_threashold - (static-1.5) *10
    T_sa_adjust = T_sa + (static-1.5) *10
    a = 0.0015; b = -0.1845; c = 6.2675
    if T_sa >= adj_threashold:
        pump_speed = 0.6
    else:
        pump_speed = a*T_sa_adjust**2 + b*T_sa_adjust + c
    return pump_speed

def pump_power_from_speed(freq, hp=25, eff=0.9):
    """Calculates the chw pump power(kW) from the speed

    Args:
        freq (float): pump speed in ratio, [0,1]
        hp (int, optional): horsepower of the pump. Defaults to 25, can change to other reasonable values.
        eff (float, optional): pump nominal efficiency. Defaults to 0.9, can change to other reasonable values.

    Returns:
        float: pump power in kW
    """
    a = 1.0608; b = -0.1222; c = 0.0684; d = 0.0022
    Pratio = a*freq**3 + b*freq**2 + c*freq + d
    pump_power = Pratio*hp*0.7457/eff
    return pump_power
