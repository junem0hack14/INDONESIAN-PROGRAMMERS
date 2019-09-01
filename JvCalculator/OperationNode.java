import java.util.ArrayList;
import java.util.Arrays;

public class OperationNode extends Node {
    /**
     * This class contains attributes of nodes used for storing operations.
     * */

    // Initialising private attributes of OperationNode class
    static String [] possibleOperations = {"*", "-", "+", "/", "%", "//", "^"};
    private static final ArrayList<String> POSSIBLE_OPERATIONS = new ArrayList<>();
    static{
        for (int i = 0; i < possibleOperations.length; i++){
            POSSIBLE_OPERATIONS.add(possibleOperations[i]);
        }
    }
    private String value;

    // Creating constructor of NumNode class
    public OperationNode(String value){
        super();
        assert POSSIBLE_OPERATIONS.contains(value);
        this.value = value;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
