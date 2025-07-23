public class q2 {
    public static Node move_Completed_Tasks(Node head){
        Node current=head,ch=null,ph=null,c=null,p=null;
        while (current!=null) {
            Node prev=current.next;
            if(current.status=="completed"){
                if(ch==null){
                    ch=current;
                    c=current;
                }
                else{
                    c.next=current;
                    c=c.next;
                }
                c.next=null;
            }
            else{
                if(ph==null){
                    ph=current;
                    p=ph;
                }
                else{
                    p.next=current;
                    p=p.next;
                }
                p.next=null;
            }
            current=prev;
        }
        if(ph==null){
            return ch;
        }
        p=ph;
        while(p.next!=null){
            p=p.next;
        }
        p.next=ch;
        return ph;
    }
    public static void main(String[] args){
        Node taskList = new Node("pending", 
                new Node("completed",
                new Node("pending",
                new Node("completed", null))));

        System.out.println("Before:");
        Node current=taskList;
        while(current!=null){
            System.out.print(current.status+current.cnt+"----->");
            current=current.next;
        }
        Node reorganized = q2.move_Completed_Tasks(taskList);
        System.out.println("null\nAfter:");
        while(reorganized!=null){
            System.out.print(reorganized.status+reorganized.cnt+"----->");
            reorganized=reorganized.next;
        }
        System.out.println("null");
    }
}
class Node {
    public String status;  // "completed" or other status
    public Node next;      // Reference to next node
    public int cnt;
    public static int tcnt=0;
    public Node(String status) {
        this.status = status;
        this.next = null;
        this.cnt=++tcnt;
    }
    
    // Optional constructor with next node reference
    public Node(String status, Node next) {
        this.status = status;
        this.next = next;
        this.cnt=++tcnt;
    }
}