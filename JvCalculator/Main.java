import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    static String [] possibleOperations = {"*", "-", "+", "/", "%", "//", "^"};
    private static final ArrayList<String> POSSIBLE_OPERATIONS = new ArrayList<>();
    static{
        for (int i = 0; i < possibleOperations.length; i++){
            POSSIBLE_OPERATIONS.add(possibleOperations[i]);
        }
    }

    private static boolean isOperation(String aStr){
        return POSSIBLE_OPERATIONS.contains(aStr);
    }

    private static boolean isNumber(String aStr){
        try{
            BigDecimal a = new BigDecimal(aStr);
        }
        catch (java.lang.NumberFormatException e){
            return false;
        }
        return true;
    }

    private static BigDecimal evaluateExpression(String expression){
        ArrayList<Node> nodes = new ArrayList<>();
        String whitespace = " ";
        String[] values = expression.split(whitespace);
        for (String value : values){
            if (isOperation(value)){
                nodes.add(new OperationNode(value));
            }
            else if (isNumber(value)){
                nodes.add(new NumNode(new BigDecimal(value)));
            }
        }

        while (nodes.size() > 1){
            BigDecimal firstNum = ((NumNode) nodes.get(0)).evaluate((OperationNode) nodes.get(1), (NumNode) nodes.get(2));
            ArrayList<Node> tempList = new ArrayList<>(); // initial value
            tempList.add(new NumNode(firstNum));
            for (int i = 3; i < nodes.size(); i++){
                tempList.add(nodes.get(i));
            }
            nodes = tempList;
        }
        return ((NumNode) nodes.get(0)).getValue();
    }

    public static void main(String[] args){
        /**
         * This function is used to run the program.
         * */

        Scanner s = new Scanner(System.in);
        int option;
        System.out.println("Enter 1 to type an expression.");
        System.out.println("Enter 2 to quit.");
        System.out.println("Please enter a number: ");
        option = s.nextInt();
        while (option < 1 || option > 2){
            System.out.println("Sorry, invalid input! Please enter a number: ");
            option = s.nextInt();
        }

        while (option != 2){
            String[] aChars = {" ", ".", "e", "1", "2", "3",
                    "4", "5", "6", "7", "8", "9", "0", "*", "-", "+", "/", "%", "//", "^"};
            ArrayList<String> allowedChars = new ArrayList<>();
            for (int i = 0; i < aChars.length; i++){
                allowedChars.add(aChars[i]);
            }
            Scanner sc = new Scanner(System.in);
            String expression;
            System.out.println("Please enter an expression: ");
            expression = sc.nextLine();
            boolean canProceed = true; // initial value
            for (int i = 0; i < expression.length(); i++){
                if (!allowedChars.contains(expression.substring(i, i + 1))) {
                    canProceed = false;
                    break;
                }
            }

            while (!canProceed){
                System.out.println("Sorry, invalid expression! Please enter another expression: ");
                canProceed = true; // initial value
                expression = sc.nextLine();
                for (int i = 0; i < expression.length(); i++){
                    if (!allowedChars.contains(expression.substring(i, i + 1))) {
                        canProceed = false;
                        break;
                    }
                }
            }

            BigDecimal result = evaluateExpression(expression);
            System.out.println(expression + " = " + result);

            System.out.println("Please enter a number: ");
            option = s.nextInt();
            while (option < 1 || option > 2){
                System.out.println("Sorry, invalid input! Please enter a number: ");
                option = s.nextInt();
            }
        }
    }
}
