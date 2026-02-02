import java.util.*;
import java.io.*;
public class simppleThread5 extends Thread{
	int n;
	String msg;

	simppleThread5(int n,String msg){
	this.n=n;
	this.msg=msg;
	}

	public static void main(String[]args){
		Scanner sc=new Scanner(System.in);
		simppleThread5 t1=new simppleThread5(10,"Bharat");
		t1.start();
		simppleThread5 t2=new simppleThread5(20,"Mata");
                t2.start();

		simppleThread5 t3=new simppleThread5(30,"Jay");
                t3.start();

	}
	public void run(){
		for(int i=1;i<=n;i++){
			System.out.println(msg);
		}
	}
}
