# diagram.py
from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import BigTable
from diagrams.gcp.iot import IotCore
from diagrams.gcp.storage import GCS
from diagrams.firebase import Firebase
from diagrams.generic.device import Mobile
from diagrams.onprem.analytics import Tableau

"""Cloud-Based Data Processing Pipeline for Portfolio App"""
with Diagram("Portfolio App Data Platform", show=False):
    with Cluster("Google Cloud Platform"):
        with Cluster("Fetch"):
            pipeline_refresh = Functions("periodic fetch")

        with Cluster("Data Lake"):
            bigquery = BigQuery("bigquery")
            gcs = [GCS("storage")]
            pipeline_refresh >> gcs
            gcs >> bigquery

        with Cluster("Processing"):
            cloudrun_processing = Functions("data processing")
            bigquery >> cloudrun_processing
            bigquery << cloudrun_processing

        with Cluster("Requests"):
            app_requests = Functions("app api requests")
            app_requests >> cloudrun_processing
            app_requests << cloudrun_processing

    with Cluster("Data Sources"):
        IotCore("alphavantage") >> pipeline_refresh
        IotCore("yfinance") >> pipeline_refresh

    with Cluster("App Authentication"):
        auth_layer = Firebase("app authentication")

    with Cluster("Devices"):
        mobile = Mobile("app instance")
        mobile >> auth_layer
        mobile << auth_layer
        mobile >> app_requests

"""Cloud-Based Data Processing & Analytic Pipeline"""
with Diagram("Cloud Data Pipelines", show=False):
    with Cluster("Google Cloud Platform"):
        with Cluster("Fetch"):
            pipeline_refresh = Functions("pipeline_refresh")

        with Cluster("Data Lake"):
            bigquery = BigQuery("bigquery")
            gcs = [GCS("storage")]
            pipeline_refresh >> gcs
            gcs >> bigquery

        with Cluster("Data Enrichment"):
            data_enrichment = Functions("data enrichment")
            pipeline_refresh >> data_enrichment
            data_enrichment >> gcs

    with Cluster("Data Sources"):
        IotCore("alphavantage") >> pipeline_refresh
        IotCore("yfinance") >> pipeline_refresh

    with Cluster("Dashboard"):
        Tableau("dashboard") << bigquery

        # Define the diagram

"""API & Orchestrator Integrations for B2B Commerce Ecosystem"""
# with Diagram("B2B API Integrations", show=False):
#     ELB("lb") >> EC2("web") >> RDS("userdb")

"""Global Lifesciences Healthcare Conceptual Architecture Landscape"""
# with Diagram("LSHC Architecture Blueprint", show=False):
#     ELB("lb") >> EC2("web") >> RDS("userdb")
