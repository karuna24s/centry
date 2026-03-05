class PaymentsController < ApplicationController
  # SECURITY TRAP: Hardcoded Secret (Should be in ENV)
  STRIPE_SECRET = "REPLACED_FOR_SECURITY_AUDIT_DEMO"

  def process_all_refunds
    # ARCHITECTURAL TRAP: N+1 Query
    # Fetching all refunds (1 query) then hitting DB for each 'user' (N queries)
    @refunds = Refund.where(status: 'pending')

    @refunds.each do |refund|
      Stripe::Refund.create(
        customer: refund.user.stripe_id,
        amount: refund.amount,
        api_key: STRIPE_SECRET
      )
      refund.update!(status: 'processed')
    end
  end
end
