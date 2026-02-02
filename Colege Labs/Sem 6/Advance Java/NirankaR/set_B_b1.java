import java.util.TreeSet;
import java.util.Scanner;

public class set_B_b1{
	public static void main(String[]args){
		Scanner sc=new Scanner(System.in);
		TreeSet<Object> ts=new TreeSet<>();
		System.out.println("Enter how any numbers: ");
		int n=sc.nextInt();
		System.out.println("Enter the "+n+" Numbers");
		sc.nextInt();
		for(int i=0;i<n;i++){
			int num=sc.nextInt();
			ts.add(num);
		}
		System.out.println("NUmber in sorted order  without duplicates are "+ts);
		sc.close();
	}
}
