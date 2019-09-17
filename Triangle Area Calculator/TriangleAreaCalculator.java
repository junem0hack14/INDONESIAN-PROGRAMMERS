import java.util.*;


public class TriangleAreaCalculator {
	public static void main(String[] args) {
		Scanner s = new Scanner(System.in);
		double sideA, sideB, angleAB;
		System.out.println("Please enter length of side A: ");
		sideA = s.nextDouble();
		System.out.println("Please enter length of side B: ");
		sideB = s.nextDouble();
		System.out.println("Please enter size of angle between sides A and B in degrees: ");
		angleAB = s.nextDouble();
		double area = 0.5 * sideA * sideB * Math.sin(angleAB * Math.PI / 180);
		System.out.println("Area of triangle = " + area + " square units.");
	}
}
