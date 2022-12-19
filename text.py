welcome_message = """Hey there! \n \
    
    Firstly we'd like to say a big thank you for submitting your app '{0}' to become a member of our growing ecosystem! Your submission has passed our automatation service's checks so were ready to start the review process for your app.\n \
    
    We'll use this ticket as our means of communication so please feel free to comment here if you have any questions or concerns.\n \

    Submissions fall into an internal queue and are processed chronoligically, processing times vary depending on queue load but are *typically completed within 10 business days*.\
    The ticket will be assigned to an engineer who will then begin the review, this ticket won't be updated until after this time.\n \

    The review process is broken down into 3 parts:\n \

    *Design/Functionality*\n \

    We check the design elements of the app's menus and components for consistency, and ensure that the app functions as advertised. More details of what's expected can be found in our [public guidelines|https://developers.miro.com/docs/design-guidelines].
    The Design review will be performed on a Miro board which will be shared with you once the review has started, you will given access to comment and so will be able to collaborate with the team.\n \

    *Security*\n \

    We check for things like the presence of security headers and HSTS on your server hosting the app. More details can be found in our [public guidelines|https://developers.miro.com/docs/security-guidelines].
    Once the security review has been completed one of our security engineers will add document with the results to the ticket. 
    \n \

    *Marketing*\n \

    This is for the app listing that will be present on the [Miro Marketplace|https://miro.com/marketplace/] once the app is approved. Please fill out and submit the below form and our Product Marketing Manager will be in touch if there are any changes needed.\n \

    [Miro Marketplace App Listing Submission form|https://miro-survey.typeform.com/to/lspd7BzP]\n \

    Please refer to our [Marketplace Listing Guidelines|https://developers.miro.com/docs/marketplace-listing-guidelines] for more details. 

    We'll be in touch to let you know the outcomes of each stage and if we have any questions or encounter issues.\n \
    
    Cheers,\n \
    
    Miro Marketplace Team
    """

failure_message = """Thanks for submitting your app to the Miro Marketplace!\n \

 I'm afraid our automation has encountered some initial issues with the values you've provided on the submission form. These are outlined below:\n \
 
 {0}\n \

 Please take a look at the highlighted issues and provide us with updated values.\n \

 Cheers,\n \

 Miro Marketplace Team."""

review_started_message = """Hello again! \n \

    We've just kicked off the review process for your app '{0}', as mentioned in our previous comment this consists of *Security* and *Design* checks.  \n \

    A ticket has automatically been created with our Security team who will run checks against the public [App Security Guidelines|https://developers.miro.com/docs/security-guidelines]. *It's important you ensure your app's hosting infrastructre is inline with these guidelines otherwise the submission will be rejected*. 

    The Design review will take place on the Miro Board linked below, this review will be performed against the public [App Design Guidelines|https://developers.miro.com/docs/design-guidelines]. You should have been granted access to this board, please add any comments you may have throughout the review.  \n \

    [Miro Design App Review Board|{1}] \n \

    Don't hestitate to add a comment here if you have any further questions! \n \

    Cheers,\n \

    Miro Marketplace Team."""