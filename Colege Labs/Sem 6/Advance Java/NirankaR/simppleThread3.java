import java.io.*;
class simppleThread3 extends Thread{
	public static void main(String[]args){
	simppleThread3 t=new simppleThread3();
	t.start();
	}
	public void run(){
		try{
		for(char ch='A';ch<='Z';ch++){
			System.out.println(ch);
			sleep(2000);
		}
	}
	catch(Exception e){
	System.out.println(e);
	}

	}
}
