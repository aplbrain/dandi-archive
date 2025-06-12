# Design private and embargoed data into a private bucket.  

## Context

EMBER needs to host three classes of data:
1. class I: publicly accessible open data
2. class II: restricted access data (including de-identified data)
3. class III: sensitive human and animal data (including PHI/PII)

For further descriptions of these classes, see our [BBQS-EMBER-Data-Model repository](https://github.com/aplbrain/BBQS-EMBER-Data-Model/tree/main/EMBER_Classes)

Classes I and II data will be hosted in EMBER-DANDI, while class III data will be hosted in a separate system, EMBERvault.

In order to store class II data, EMBER-DANDI will need the ability to have permanently private dandisets, in contrast to embargoed dandisets, which are only temporarily private. These private dandisets will therefore need to be stored in a private S3 bucket (not the Open Data bucket).

## Requirements

- Private dandisets and Embargo dandisets cannot be stored in the Open Data bucket 
- Leave the current embargo system in place (to enable new features to be merged back into DANDI, if desired)
   - i.e. we need to allow for embargoed data to be stored either in the public open data bucket (as in DANDI) or in the new private bucket (as EMBER requires)

## Design

1. We will add two new variables to the DANDI system. (set in dandi-infrastructure)
   * AllowPrivateDandisets = (default to `False`)
     * A value of `True` will enable the private S3 bucket and the ability to set data as private
   * UsePrivateBucketForEmbargoedData = (default to False)  This requires that AllowPrivateDandiSets be True.
     * A value of `True` will store embargoed data in the private S3 bucket

1. We will create a new bucket (in dandi-infrastructure) for private data, as well as a corresponding log bucket.

1. We will add `EmbargoStatus.PRIVATE` as an enum value (in dandi-archive)
   * This value will indicate a permanently private dandiset
   * Current definition of `EmbargoStatus` class: https://github.com/dandi/dandi-archive/blob/2ac48ebd7ad32607d155da4916ce3aa8d0a4d562/dandiapi/api/models/dandiset.py#L13

1. Use S3 Batch operation for copying data over and AWS Lambda function(s) for monitoring and handling errors

### Re-Design of Unembargo Procedure

A diagram of the unembargo procedure (pertaining to just the objects) is shown below

```mermaid
sequenceDiagram
    autonumber
    participant Client
    participant Server
    participant Worker
    participant S3

    Client ->> Server: Unembargo dandiset
    Server ->> Worker: Dispatch unembargo task
    Worker ->> S3: List of all dandiset objects are aggregated into a manifest
    Worker ->> S3: S3 Batch Operation job created
    S3 ->> Worker: Job ID is returned
    Worker ->> Server: Job ID is stored in the database
    S3 ->> S3: Tags on all objects in the supplied manifest are removed and each object is copied out of the private bucket to the public.
    Note over Worker,S3: After some time, am AWS lambda function is run <br> which checks the status of the S3 job
		Worker ->> Server: Job ID is retrieved
    Worker ->> S3: Job status retrieved, worker observes that <br> the job has finished and was successful
    Worker ->> S3: If job had copy errors create a new S3 Batch Operation Job using the list of failures, Jump back up to S3 returns Job ID

    Worker ->> Server: Job ID is cleared, dandiset embargo status is set to OPEN

    rect rgb(179, 209, 95)
        Client ->> S3: Data is now publicly accessible
    end
```
