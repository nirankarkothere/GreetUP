import java.util.*;
import java.io.*;
class simppleThread6 extends Thread{
public static void main(String[]args){
	simppleThread56t=new simppleThread6();
	t.start();
}
public void run(){
	for(int i=1;i<10;i++){
	Random r=new Random();
	int n=r.nextInt(50);
	System.out.println(n);
	}
}
}
