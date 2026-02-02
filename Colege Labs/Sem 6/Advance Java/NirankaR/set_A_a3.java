import java.util.Scanner;
import java.util.TreeSet;

public class set_A_a3{
	public static void main(String[]args){
		Scanner sc=new Scanner(System.in);
		TreeSet<String> ts=new TreeSet<>();
		System.out.println("How many colors you waant to insert: ");
		int n=sc.nextInt();

		System.out.println("Enter the colors name: ");
		sc.nextLine();
		for(int i =0; i<n;i++){
			String c=sc.nextLine();
			ts.add(c);
		}

		System.out.println("Coloer name in Tree set: "+ts);
		ts.clear();
		sc.close();
		System.out.println("Color after removing :"+ts);
		
	}
}
