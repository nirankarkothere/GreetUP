import java.io.*;
import java.util.Hashtable;
import java.util.Scanner;
public class set_B_b3{
	public static void main(String[]args){
		try{
			File f=new File("b3.txt");
			BufferedReader br= null;
			br=new BufferedReader(new FileReader(f));
			Hashtable <String,String> table= new Hashtable<>();

			Scanner sc=new Scanner(System.in);
			String file="";
			while((file=br.readLine())!=null){
				String [] parts=file.split("");
				String name=parts[0].trim();
				String number=parts[1].trim();

				if(name.equals("")&&!number.equals("")){
					table.put(name,number);
				}

		}

		System.out.println("ENter name :");
		String key=sc.nextLine();
		if(table.containsKey(key)){
			System.out.println(table.get(key));
			br.close();
			sc.close();
		}

}
catch(Exception e){
	System.out.println(e);
}
}
}
