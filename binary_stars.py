def true_anomaly(phase, eccentricity, delta=1.0e-6):
    """
    solve for true anomaly if given the orbital phase

    phase = (t-To)/P is the phase (should be between 0 and 1)

    To = time of periastron passage
    P = orbital period

    mean_anomaly = 2*pi*phase

    eccentric_anomaly in radians

    see sec 8.8 in Marion, Classical Dynamics of Particles and Systems

    :return true_anomaly, eccentric_anomaly
    """
    import numpy as np
    mean_anomaly = 2.0 * np.pi * phase
    eccentric_anomaly = float(mean_anomaly)
    diff = 1.0
    while np.abs(diff) > delta:
        ecctest = eccentric_anomaly
        # print "{0:3.1e},{1:3.1e}".format(diff, ecctest)
        eccentric_anomaly = mean_anomaly + eccentricity * np.sin(ecctest)  # Kepler's equations
        diff = ecctest - eccentric_anomaly
    true_anomaly = 2.0 * np.arctan(
        np.sqrt((1.0 + eccentricity) / (1.0 - eccentricity)) * np.tan(eccentric_anomaly / 2.0))
    if true_anomaly < 0.0:
        true_anomaly = true_anomaly + 2.0 * np.pi
    return true_anomaly, eccentric_anomaly  # True anomaly in radians


def ta2phase(true_anomaly, eccentricity, delta=1.0e-6):
    """
    Given a true anomaly and eccentricity, calculate the phase (=Mean anomaly/2pi)
    using the Kepler Equation:

    tan(true_anomaly/2) = sqrt((1+e)/(1-e)) tan E/2
    and
    Mean Anomaly = E - e sin E

    where E is the eccentric anomaly
    and true_anomaly is in radians
    """
    import numpy as np
    e = eccentricity
    eccentric_anomaly = 2.0 * np.arctan(np.sqrt((1 - e) / (1 + e)) * np.tan(true_anomaly / 2.0))
    if eccentric_anomaly < 0:
        eccentric_anomaly = eccentric_anomaly + 2.0 * np.pi
    mean_anomaly = eccentric_anomaly - e * np.sin(eccentric_anomaly)
    if mean_anomaly < 0:
        mean_anomaly = mean_anomaly + 2.0 * np.pi
    phase = mean_anomaly / (2.0 * np.pi)
    return phase