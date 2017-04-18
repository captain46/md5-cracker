package redis;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

import redis.clients.jedis.*;

public class RedisTest {

	public static void main(String[] args) {
	
		Jedis jedis = new Jedis("localhost");
		
		try {
			File file = new File("txt/passwoerter.txt");
			FileReader fileReader = new FileReader(file);
			BufferedReader in = new BufferedReader(fileReader);
			String[] keyVal; 
			String line;
			while((line = in.readLine()) != null)
			{
				keyVal = line.split(";");
				
				if(keyVal.length > 1)
				{
					jedis.set(keyVal[1], keyVal[0]);
				}
				
				System.out.println(jedis.get(keyVal[1]));
			}
		} catch (Exception e) {
			System.out.println("Error reading textfile");
		}
		
		
	}

}
