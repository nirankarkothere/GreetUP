import java.io.*;
class simppleThread extends Thread{
	public static void main(String[]args){
	//	Thread t=new Thread(new tdemo());
		simppleThread h=new simppleThread();
	h.start();	
} 

public void run(){
	System.out.println("Hello guys welcome to my blog");
}
}
