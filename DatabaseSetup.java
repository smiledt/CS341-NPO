import java.sql.Connection;
import java.sql.SQLException;
import java.util.Scanner;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class DatabaseSetup {
	private String url = "jdbc:sqlite:/Users/craigglassbrenner/Desktop/Projects/CS341-NPO/BookKeepingDB.db";
	private Connection connection;
	
	public DatabaseSetup() {}
	
	public void connect() throws SQLException {
		connection = DriverManager.getConnection(url);
	}
	
	public void disconnect() throws SQLException {
		connection.close();
	}
	
	public ResultSet runQuery(String query) throws SQLException {
		PreparedStatement stmt = connection.prepareStatement(query);
		ResultSet results = stmt.executeQuery();
		
		return results;
	}

	public boolean addAccount(String firstName, String lastName, String email, String phoneNumber, 
			String jobTitle, int numDonations, int numEventsVolunteeredFor, Scanner s) throws SQLException {
			
		connection = DriverManager.getConnection(url);
		
		String query = "SELECT email FROM Users WHERE email LIKE '" + email + "'";
		ResultSet results = runQuery(query);
		
		if(results.getRow() != 0 ) {
			System.out.println("Email already exists, can't create another account.");
			return false;
		}
		System.out.print("\nPassword: ");
		String password = s.next();
		
		query = "INSERT INTO Users VALUES('" + firstName + "', '" +
				  lastName + "', '"  + email + "', '"  + phoneNumber + "', '" + jobTitle + "', "
				  + numDonations + ", " + numEventsVolunteeredFor + ", '" + password + "')";
		
		PreparedStatement stmt = connection.prepareStatement(query);
		stmt.execute();
		
		s.close();
		
		return true;
	}
}
