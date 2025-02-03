import java.util.List;
import java.util.ArrayList;
// Abstract class for managing appointments
abstract class AppointmentManager {
    List<String> appointments;

    AppointmentManager() {
        this.appointments = new ArrayList<>();
    }

    abstract void scheduleAppointment(String date);

    void displayAppointments() {
        System.out.println("Appointments:");
        for (String appointment : appointments) {
            System.out.println("- " + appointment);
        }
    }
}
