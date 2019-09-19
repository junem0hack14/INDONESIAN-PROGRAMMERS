public class Main {
	public static void main(String[] args) {
		Node a = new Node(new String("1"), new String("a"));
		a.put(new Integer(2), new String("b"));
		a.put(new Integer(3), new String("c"));
		System.out.println(a.toString());
		a.put(new Integer(3), new Integer(555));
		System.out.println(a.toString());
		System.out.println(a.remove(new Integer(3)));
		System.out.println(a.toString());
	}
}


class Node{
	/**
	* This class contains attributes of a node.
	*/
	
	// Initialising private attributes of Node class.
	private Object key;
	private Object value;
	private Node next;
	private Node previous;
	
	public Node(Object key, Object value){
		this.key = key;
		this.value = value;
		this.next = null;
		this.previous = null;
	}
	
	public Object getKey(){
		return key;
	}
	
	public void setKey(Object key){
		this.key = key;
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
	
	public Object getNextKey(){
		return this.next.getKey();
	}
	
	public Object getPreviousKey(){
		return this.previous.getKey();
	}
	
	public Object getNextValue(){
		return this.next.getValue();
	}
	
	public Object getPreviousValue(){
		return this.previous.getValue();
	}
	
	private boolean keyExists(Object key){
		Node currNode = this;
		while (currNode.previous != null){
			currNode = currNode.previous;
		}
		
		while (currNode.next != null){
			if (currNode.key.equals(key)){
				return true;
			}
			currNode = currNode.next;
		}
		
		return false;
	}
	
	public void put(Object key, Object value){
		Node correspondingNode = null; // initial value
		Node currNode = this; // initial value
		if (keyExists(key)){
			// Getting the node with the corresponding key
			while (currNode.previous != null){
				currNode = currNode.previous;
			}
			
			while (!currNode.key.equals(key)){
				currNode = currNode.next;
			}
			
			correspondingNode = currNode;
			correspondingNode.setValue(value);
		}
		else{
			while (currNode.next != null){
				currNode = currNode.next;
			}
			
			currNode.next = new Node(key, value);
			currNode.next.previous = this;
		}
	}
	
	public boolean remove(Object key){
		if (!keyExists(key)){
			return false;
		}
		
		Node currNode = this;
		while (currNode.previous != null){
			currNode = currNode.previous;
		}
		
		while (currNode.next != null){
			if (currNode.key.equals(key)){
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
	
	public boolean isEqualTo(Node node){
		return key.equals(node.key) && value.equals(node.value) && next.equals(node.next) && previous.equals(node.previous);
	}
	
	public String toString(){
		String res = "{"; // initial value
		Node currNode = this;
		while (currNode.previous != null){
			currNode = currNode.previous;
		}
		
		while (currNode != null){
			res += currNode.next == null ? currNode.key.toString() + ": " + currNode.value.toString() : currNode.key.toString() + ": " + currNode.value.toString() + ", ";
			currNode = currNode.next;
		}
		
		res += "}";
		return res;
	}
}
