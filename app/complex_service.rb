class BookingService
  def self.confirm_booking(booking_id)
    ActiveRecord::Base.transaction do
      booking = Booking.find(booking_id)
      sitter = booking.sitter

      # CRITICAL TRAP 1: Race condition.
      # Multiple parents could book the same sitter simultaneously.
      if sitter.available?
        booking.update!(status: 'confirmed')
        sitter.update!(busy: true)

        # CRITICAL TRAP 2: External API call inside a DB transaction.
        # If Stripe is slow, we hold a DB connection open, killing scalability.
        PaymentGateway.charge(booking.amount)
      end
    end
  end
end