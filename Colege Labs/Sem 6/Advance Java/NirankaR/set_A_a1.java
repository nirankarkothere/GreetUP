import java.util.*;
public class set_A_a1{
	public static void main(String[]args){
	Scanner sc=new Scanner(System.in);
	ArrayList<String> list=new ArrayList<>();
	System.out.println("Enter how many cites to insert : ");
	int n=sc.nextInt();
        System.out.println("Enter cites Name : ");
	sc.nextLine();

	for(int i=0;i<n;i++){
		String c=sc.nextLine();
		list.add(c);
		}

        System.out.println("Array List after Adding the element: ");
        
        
        
        /*for(int  i=0;i<n;i++){
                System.out.println(list);
                }*/
        System.out.println(list);
        System.out.println("Array List after removing the element: ");
	list.clear();
	System.out.println(list);
	sc.close();
	}

}
