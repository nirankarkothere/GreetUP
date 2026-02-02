import java.util.*;
public class set_A_a2{
	public static void main(String[]args){
		Scanner sc=new Scanner(System.in);
		LinkedList<String> ll=new LinkedList<>();
		System.out.println("Enter how many Friends ");
		int n=sc.nextInt();

		System.out.println("Enter the name of "+n+" Friends :");
		sc.nextLine();
		for(int i=0;i<n;i++){
			String name=sc.nextLine();
			ll.add(name);
		}
		System.out.println("Linked lIst After adding the friends are :");
		System.out.println(ll);
		System.out.println("Linked lIst After removing the friends are :");
                ll.clear();
		System.ou.println(ll);
		sc.close();

	}
}
