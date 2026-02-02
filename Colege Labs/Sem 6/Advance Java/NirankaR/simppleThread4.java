import java.io.*;
import java.util.*;
public class simppleThread4 extends Thread{

	int n;
	String msg;
	simppleThread4(int n,String msg){
		this.n=n;
		this.msg=msg;
	}
	public static void main(String[]args){
	Scanner sc=new Scanner(System.in);
        System.out.println("Enter the value of n :");
        int n=sc.nextInt();
        System.out.println("Enter the Message :");
        String msg=sc.next();
	simppleThread4 t=new simppleThread4(n,msg);
	t.start();
}


public void run(){	
	for(int i=1;i<=n;i++){
		System.out.println(msg);
	}

}
}
