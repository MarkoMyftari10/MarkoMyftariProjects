

import java.util.List;
import java.util.ArrayList;

class Physiotherapist extends Person implements ExerciseManagement {
    private List<String> exercises;

    Physiotherapist(String name, int age) {
        super(name, age);
        this.exercises = new ArrayList<>();
    }

    @Override
    void displayInfo() {
        System.out.println("Physiotherapist: " + name + ", Age: " + age);
    }

    @Override
    public void addExercise(String exercise) {
        exercises.add(exercise);
        System.out.println("Exercise added: " + exercise);
    }

    @Override
    public void displayExercises() {

    }

    @Override
    public List<String> getExercises() {
        return exercises;
    }
}
