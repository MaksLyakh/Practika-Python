from models.entities import Appointment, Patient, Doctor
from models.enums import AppointmentType


class AppointmentFactory:

    PRICES = {
        AppointmentType.THERAPY: 1500,
        AppointmentType.DIAGNOSTIC: 2500,
        AppointmentType.CONSULTATION: 2000
    }

    def create_appointment(
        self,
        appointment_id: int,
        patient: Patient,
        doctor: Doctor,
        appointment_type: AppointmentType
    ) -> Appointment:

        if appointment_type not in self.PRICES:
            raise ValueError("Неизвестный тип медицинского приёма")

        price = self.PRICES[appointment_type]

        return Appointment(
            id=appointment_id,
            patient=patient,
            doctor=doctor,
            appointment_type=appointment_type,
            price=price
        )
