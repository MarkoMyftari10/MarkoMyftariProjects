import java.util.List;

// Interface for managing exercises
interface ExerciseManagement {
    void addExercise(String exercise);
    void displayExercises();

    List<String> getExercises();
}

