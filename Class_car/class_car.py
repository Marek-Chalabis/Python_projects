import class_car_exception


class Car:
    """
    Car - class operating on cars
    """

    def __init__(self, pax_count, car_mass, gear_count):
        """
            :param pax_count: :  number of passengers riding in the car (including the driver)
            :param car_mass: mass of the empty car (in kg)
            :param gear_count:  number of gears
        """
        self.pax_count = pax_count
        self.car_mass = car_mass
        self.gear_count = gear_count

    @property
    def total_mass(self):
        """ Returns the total mass estimate of a car instance, assuming that an average person weight is 70 kg"""
        return self.car_mass + self.pax_count * 70

    @property
    def pax_count(self):
        return self._pax_count

    @pax_count.setter
    def pax_count(self, value):
        """checks number of passengers riding in the car (including the driver) if they are in range 1-5"""
        self._check_inputs(value)

        if value > 5 or value < 1:
            raise class_car_exception.IllegalCarError(
                value,
                "Number of passengers riding in the car (including the driver) "
                "cannot be greater than 5, or less than 1",
            )
        else:
            self._pax_count = value

    @property
    def car_mass(self):
        return self._car_mass

    @car_mass.setter
    def car_mass(self, value):
        """checks if car_mass is less or equal to 2000"""
        self._check_inputs(value)

        if value > 2000:
            raise class_car_exception.IllegalCarError(
                value,
                "Mass of the empty car in kg  (excluding the passengers) "
                "cannot be greater than 2000 kg",
            )
        self._car_mass = value

    @property
    def gear_count(self):
        return self._gear_count

    @gear_count.setter
    def gear_count(self, value):
        self._check_inputs(value)

        self._gear_count = value

    def _check_inputs(self, value):
        """
        Checks inputs
            :param value: : value to check
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Inputs needs to be a integer or float")
        elif value < 0:
            raise ValueError("Value can't be negative")
