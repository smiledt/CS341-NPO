import java.sql.SQLException;
import java.util.Scanner;

public class Admin {
	String email;
	String firstName;
	String lastName;
	String phoneNumber;
	
	public Admin() {
		super();
	}
	
	public boolean createAccount() throws SQLException {
		DatabaseSetup db = new DatabaseSetup();
		
		Scanner scan = new Scanner(System.in);
		
		System.out.print("Position to Create Account For: ");
		String jobTitle = scan.next();
		jobTitle = jobTitle.toLowerCase();
		
		if(jobTitle.compareTo("volunteer") != 0 && jobTitle.compareTo("donor") != 0 && jobTitle.compareTo("admin") != 0) {
			System.out.println("Not a valid job title...");
			scan.close();
			return false;
		}
		
		System.out.print("\nFirst Name: ");
		String firstName = scan.next();
		System.out.print("\nLast Name: ");
		String lastName = scan.next();
		System.out.print("\nEmail: ");
		String to_add_email = scan.next();
		System.out.print("\nPhone Number: ");
		String phoneNumber = scan.next();
		
		return (db.addAccount(firstName, lastName, to_add_email, phoneNumber, jobTitle, 0, 0, scan));
		
	}
	
	public String getFirstName() {
		return firstName;
	}
	public void setFirstName(String f) {
		firstName = f;
	}
	public String getLastName() {
		return lastName;
	}
	public void setLatName(String l) {
		lastName = l;
	}
	public String getEmail() {
		return email;
	}
	public void setEmail(String e) {
		email = e;
	}
	public String getPhoneNumber() {
		return phoneNumber;
	}
	public void setPhoneNumber(String p) {
		phoneNumber = p;
	}
	
}
