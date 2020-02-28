import java.sql.SQLException;

public class Driver {
	static DatabaseSetup db;

	public static void main(String[] args) throws SQLException {
		
		db = new DatabaseSetup();
		
		try {
			db.connect();
		} catch (SQLException e) {
			System.out.println("Unable to connect.");
			e.printStackTrace();
		}
		System.out.println("Connected.");
		
		Admin a = new Admin();
		boolean b = a.createAccount();
		if(b == true) {
			System.out.println("Account Creation Successful.");
		}
		
		try {
			db.disconnect();
		} catch (SQLException e) {
			System.out.println("Can't disconnect.");
		}
		System.out.println("Disconnected.");
		
	}

}
