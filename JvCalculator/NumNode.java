import java.math.BigDecimal;
import java.math.RoundingMode;

public class NumNode extends Node {
    /**
     * This class contains attributes of nodes used for storing numbers.
     * */

    // Initialising private attribute of NumNode class
    private BigDecimal value;

    // Creating constructor of NumNode class
    public NumNode(BigDecimal value){
        super();
        this.value = value;
    }

    public BigDecimal getValue() {
        return value;
    }

    public void setValue(BigDecimal value) {
        this.value = value;
    }

    public BigDecimal evaluate(OperationNode operationNode, NumNode numNode){
        return operationNode.getValue().equals("*") ? value.multiply(numNode.value) : operationNode.getValue().equals("-") ?
                value.subtract(numNode.value) : operationNode.getValue().equals("+") ? value.add(numNode.value) :
                operationNode.getValue().equals("/") ? value.divide(numNode.value, 100, RoundingMode.FLOOR) :
                operationNode.getValue().equals("%") ? value.remainder(numNode.value) :
                operationNode.getValue().equals("//") ? value.divide(numNode.value, 0, RoundingMode.FLOOR) :
               new BigDecimal(Math.pow(value.doubleValue(), numNode.value.doubleValue()));
    }
}
