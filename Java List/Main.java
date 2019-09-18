public class Main {
	public static void main(String[] args) {
		Node a = new Node(5);
		a.add(7);
		a.add("s");
		a.add("k");
		System.out.println(a.toString());
		a.remove("s");
		System.out.println(a.toString());
		a.add(13);
		System.out.println(a.toString());
	}
}


class Node{
	/**
	* A class containing attributes of a Node.
	*/
	
	// Initialising private attributes of Node class
	private Object value;
	private Node next;
	private Node previous;
	
	public Node(Object value){
		this.value = value;
		this.next = null;
		this.previous = null;
	}
	
	public Object getValue(){
		return value;
	}
	
	public void setValue(Object value){
		this.value = value;
	}
	
	public Node getNext(){
		return this.next;
	}
	
	public void setNext(Node next){
		this.next = next;
	}
	
	public Node getPrevious(){
		return this.previous;
	}
	
	public void setPrevious(Node previous){
		this.previous = previous;
	}
	
	public Object getNextValue(){
		return this.next.getValue();
	}
	
	public Object getPreviousValue(){
		return this.previous.getValue();
	}
	
	public void add(Object object){
		Node currNode = this;
		while (currNode.next != null){
			currNode = currNode.next;
		}
		
		currNode.next = new Node(object);
		currNode.next.previous = this;
	}
	
	public boolean remove(Object object){
		Node currNode = this;
		while (currNode.previous != null){
			currNode = currNode.previous;
		}
		
		while (currNode.next != null){
			if (currNode.value.equals(object)){
				if (currNode.next != null){
					currNode.next.previous = currNode.previous;
				}
				if (currNode.previous != null){
					currNode.previous.next = currNode.next;
				}
				
				return true;
			}
			currNode = currNode.next;
		}
		return false;
	}
	
	public String toString(){
		String res = "["; // initial value
		Node currNode = this;
		while (currNode.previous != null){
			currNode = currNode.previous;
		}
		
		while (currNode != null){
			res += currNode.next == null ? currNode.getValue().toString() : currNode.getValue().toString() + ", ";
			currNode = currNode.next;
		}
		
		res += "]";
		return res;
	}
}
