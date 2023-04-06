---
layout: page
title: ABCs of the Digital Certificates with Public Key Infrastructures (PKI)
description: Comparison of Digital Certificates in the chain of trust of a website, Man-in-the-middle (MITM) Scenarios involving Digital Certificates
img: assets/files/iith/projects/pki/certificate.png
importance: 1
category: pki
---




<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/files/iith/projects/pki/certificate.png" title="compare" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Quantitative Comparison between different frameworks
</div>

PART-A: 

Comparison of Digital Certificates in the chain of trust of a website

1. Visit the website #N in this list of top-100 most visited websites globally where is #N is
the last two digits in your roll number and download all the certificates in .CER format in
the chain of trust from the root Certificate, intermediate certificate(s), to the end-user
(website) certificate at the leaf in the hierarchy

2. Answer the following queries after filling out the above table:
    1. Which certificate type (DV/OV/IV/EV) is more trustable and expensive?
    2. What is the role of Subject Alternative Name (SAN) field in X.509 certificate?
    3. Why are key usages and basic constraints different for root, intermediate and end
    certificates?
    4. What is the difference between Signature value and Thumbprint of a digital certificate?
    5. Why do RSA key lengths increase over the years? Why is ECDSA being preferred over
    RSA now-a-days?
    6. What are pros and cons of pre-loading root and intermediate certificates in the root
    stores of browsers and OSes?
    7. Why are root CAs kept offline?
    8. List out names of OS/Browser/Company whose root stores pre-populated with Root and
    Intermediate CA certificates of the website #N?


PART-B
1. You have received the digital certificate of the website #N over email. How do you verify
whether the certificate is valid without using any online tools or browsers? Write a
psuedo-code of your verifier function named myCertChecker( ) and explain how it works
by picking the entire chain of trust of an end-user cert (of the website #N) in PART-A of
this assignment.
2. Consider the scenario in which evil Trudy has used the digital certificate of the website
(Bob) named abc.com to launch her own web server with the domain name, xyz.com.
Does your function myCertChecker( ) returns valid or invalid for this when someone like
Alice tries to access Trudy's website xyz.com from a browser like Chrome/Edge/Firefox?
3. Consider the scenario in which evil Trudy has used the digital certificate of Bob's website
abc.com to launch her own web server with the domain name, xyz.com. When a web
client (Alice) tries to connect with Bob’s website abc.com by sending a DNS query, Trudy
responds with her IP address by launching MITM attack (What is DNS cache poisoning?
| DNS spoofing | Cloudflare) Does your function myCertChecker( ) returns valid or invalid
for this and what are the consequences? What kind of attacks can Trudy launch in this
scenario?


<div class="row">
    <div class="col-sm-12 clearfix">
        <ul class="nav nav-pills">
            <a href="/assets/files/iith/projects/pki/Q.pdf"><button type="button" class="btn btn-outline-primary">PROJECT DETAILS</button></a>
            <a href="/assets/files/iith/projects/pki/A.pdf"><button type="button" class="btn btn-outline-primary">REPORT</button></a>
            <a href="/assets/files/iith/projects/pki/certificate_checker.py"><button type="button" class="btn btn-outline-primary">CERTIFICATE CHECKER</button></a>
        </ul>
    </div>
</div>