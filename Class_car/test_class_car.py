import class_car
import pytest
import class_car_exception


class TestCar:
    # correct object to test
    correct_object_to_test = class_car.Car(3, 1600, 5)

    def test_attributes(self):
        # create object
        assert self.correct_object_to_test.pax_count == 3
        assert self.correct_object_to_test.car_mass == 1600
        assert self.correct_object_to_test.gear_count == 5

    @pytest.mark.parametrize(
        "wrong_pax_count, car_mass, gear_count", [(6, 1500, 5), (0, 1500, 5)]
    )
    def test_incorrect_positive_values_for_pax_count(
        self, wrong_pax_count, car_mass, gear_count
    ):
        with pytest.raises(class_car_exception.IllegalCarError):
            class_car.Car(wrong_pax_count, car_mass, gear_count)

    def test_incorrect_negative_value_for_pax_count(self):
        with pytest.raises(ValueError):
            class_car.Car(-5, 1500, 5)

    @pytest.mark.parametrize(
        "pax_count, wrong_car_mass, gear_count",
        [(3, 21500, 5), (3, 3000, 5), (3, 2001, 5)],
    )
    def test_incorrect_values_for_car_mass(self, pax_count, wrong_car_mass, gear_count):
        with pytest.raises(class_car_exception.IllegalCarError):
            class_car.Car(pax_count, wrong_car_mass, gear_count)

    @pytest.mark.parametrize(
        "pax_count, car_mass, gear_count, total_mass",
        [
            (3, 1000, 5, 3 * 70 + 1000),
            (5, 1000, 5, 5 * 70 + 1000),
            (5, 1500, 5, 5 * 70 + 1500),
        ],
    )
    def test_property_total_mass(self, pax_count, car_mass, gear_count, total_mass):
        obj_to_test = class_car.Car(pax_count, car_mass, gear_count)
        assert obj_to_test.total_mass == total_mass

    def test_changing_attributes_on_object(self):

        with pytest.raises(class_car_exception.IllegalCarError):
            self.correct_object_to_test.pax_count = 16

        with pytest.raises(class_car_exception.IllegalCarError):
            self.correct_object_to_test.car_mass = 2001

    @pytest.mark.parametrize(
        "pax_count, car_mass, gear_count", [({}, 1000, 5), (5, [], 5), (5, 1500, set())]
    )
    def test_wrong_inputs(self, pax_count, car_mass, gear_count):
        with pytest.raises(TypeError):
            class_car.Car(pax_count, car_mass, gear_count)


def test_IllegalCarError():
    # test custom exception
    object_test1 = class_car_exception.IllegalCarError(1337, "TEST")
    assert object_test1.__str__() == "TEST\nGIVEN VALUE: 1337"
