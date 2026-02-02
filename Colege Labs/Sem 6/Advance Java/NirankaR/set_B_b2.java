import java.util.HashMap;
import java.util.TreeMap;
public class set_B_b2{
	public static void main(String[]args){
	HashMap<String,Integer>map=new HashMap<>();
	map.put("NIrankar",2005);
	map.put("Omkar",4008);
	map.put("Shoyeb",2004);

	System.out.println("Hash map before sorting "+map);
	TreeMap<Object,Object> tm=new TreeMap<>(map);
        System.out.println("Hash map after  sorting "+tm);

	}
}
