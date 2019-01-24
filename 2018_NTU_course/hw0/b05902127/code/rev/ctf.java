import java.util.Arrays;
public class ctf{
	public static void main(String args[]){

		byte[] var3 = new byte[]{37, 5, 118, 90, -112, -13, -34, 7, 106, 102, -115, -20, -51, 0, 80, 84, -115, -3, -34, 2, 121, 84, -87, -8};
		for(int var2 = 0; var2 < var3.length; ++var2) {

			for(byte guess= -128 ; guess<127 ; guess++){
				if(var3[var2] == (byte)(guess ^ (var2 * 42 + 1 ^ 66) & 255)){
					System.out.print((char)guess);
				}
	
			}

      	}
	}
}
