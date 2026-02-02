import java.io.*;
class simppleThread2  extends Thread{
	public static void main(String[]args){
		simppleThread2 t=new simppleThread2();
		t.start();
	}
	public void run(){
		try{
		for(int i=1;i<=10;i++){
			System.out.println("this is "+i);
			Thread.sleep(2000);
		}
		}
	catch(Exception e){
		System.out.println(e);
	}	
	}
}
