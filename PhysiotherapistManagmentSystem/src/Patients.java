import java.util.ArrayList;
import java.util.List;

// Class representing a patient
class Patient extends Person {
    int patientId;
    List<String> appointments;

    Patient(String name, int age, int patientId) {
        super(name, age);
        this.patientId = patientId;
        this.appointments = new ArrayList<>();
    }

    @Override
    void displayInfo() {
        System.out.println("Patient: " + name + ", Age: " + age + ", ID: " + patientId);
    }

    void scheduleAppointment(String date) {
        appointments.add(date);
        System.out.println("Appointment scheduled for " + date);
    }

    void displayAppointments() {
        System.out.println("Appointments:");
        for (String appointment : appointments) {
            System.out.println("- " + appointment);
        }
    }
}
