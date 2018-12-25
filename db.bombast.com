;
; BIND data file for local loopback interface
;
$TTL	604800
@	IN	SOA	ns.bombast.com. admin.bombast.com. (
			      4		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
; name servers - NS records
	IN	NS	bombast.com.
	IN	NS	verizon.com.

; name servers - A records
bombast.com.		IN	A	10.4.9.6

; 10.4.9.0/8 - A records
bombast.bombast.com.	IN	A	10.4.9.6
verizon.bombast.com.	IN	A	10.4.9.7
