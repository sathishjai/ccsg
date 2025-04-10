class Customer:
    """Customer model representing customer data"""
    
    def __init__(self, customer_data):
        """Initialize customer with data from database"""
        self.customer_id = customer_data.get('customer_id')
        self.first_name = customer_data.get('first_name')
        self.last_name = customer_data.get('last_name')
        self.address_line1 = customer_data.get('address_line1')
        self.address_line2 = customer_data.get('address_line2')
        self.city = customer_data.get('city')
        self.state = customer_data.get('state')
        self.postal_code = customer_data.get('postal_code')
        self.country = customer_data.get('country')
        self.email = customer_data.get('email')
        self.phone = customer_data.get('phone')
        self.membership_since = customer_data.get('membership_since')
        self.customer_type = customer_data.get('customer_type')
        
    def get_full_name(self):
        """Return the customer's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def get_full_address(self):
        """Return the customer's full address as a formatted string"""
        address_parts = [self.address_line1]
        
        if self.address_line2:
            address_parts.append(self.address_line2)
            
        address_parts.append(f"{self.city}, {self.state} {self.postal_code}")
        address_parts.append(self.country)
        
        return "\n".join(address_parts)
    
    def to_dict(self):
        """Convert customer data to dictionary"""
        return {
            'customer_id': self.customer_id,
            'full_name': self.get_full_name(),
            'address': self.get_full_address(),
            'email': self.email,
            'phone': self.phone,
            'membership_since': self.membership_since,
            'customer_type': self.customer_type
        }
