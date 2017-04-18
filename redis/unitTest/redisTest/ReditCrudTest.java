package redisTest;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import redis.clients.jedis.Jedis;

public class ReditCrudTest {

	

	@Test
	public void test() {
		Jedis jedis = new Jedis("localhost");
		jedis.set("testkey", "testvalue");
		
		assertTrue(jedis.get("testkey").equals("testvalue"));
		
		jedis.set("testkey", "testvalueUpdate");
		
		assertTrue(jedis.get("testkey").equals("testvalueUpdate"));
		
		jedis.del("testkey");
		
		String testval = jedis.get("testkey");
		
		assertNull(testval);
	}

}
