import os

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from fastapi import FastAPI
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider, SpanKind


class GrantonTracerError(Exception):
    """Exception for errors encountered during the tracing setup."""


class GrantonSpanProcessor(BatchSpanProcessor):
    def on_end(self, span: ReadableSpan) -> None:
        super().on_end(span=span)


class GrantonTracing:
    def __init__(self, app_insight_connection_string: str = None):
        """Initializes the GrantonTracing class to set up tracing with Azure Monitor and OpenTelemetry.

        This constructor sets up tracing based on an optional Application Insights connection string. If the connection
        string is not provided directly, the class attempts to retrieve it from the environment variables.

        Args:
            app_insight_connection_string (str, optional): Connection string for Azure Application Insights.
        """

        self.app_insight_connection_string = app_insight_connection_string
        self._setup_tracing()

    def _configure_tracer_provider(self) -> TracerProvider:
        """Configures and sets the global tracer provider.

        Initializes a TracerProvider and sets it as the global tracer provider to be used by OpenTelemetry for tracing.

        Returns:
            TracerProvider: The initialized and globally set TracerProvider instance.
        """

        tracer_provider = TracerProvider()
        set_tracer_provider(tracer_provider)
        return tracer_provider

    def _configure_azure_monitor_trace_exporter(self, connection_string: str):
        """Configures the Azure Monitor Trace Exporter using a given connection string.

        This function initializes the Azure Monitor Trace Exporter with the provided connection string and adds it to
        the global TracerProvider as a span processor.

        Args:
            connection_string (str): The connection string for Azure Monitor Trace Exporter.
        """

        exporter = AzureMonitorTraceExporter(connection_string=connection_string)
        tracer_provider = self._configure_tracer_provider()
        processor = GrantonSpanProcessor(span_exporter=exporter)
        tracer_provider.add_span_processor(span_processor=processor)

    def instrument_app(self, application: FastAPI):
        """Instruments a FastAPI application to enable tracing.

        Applies OpenTelemetry instrumentation to a given FastAPI application to enable the collection and export of
        tracing data. Raises an exception if the application is not properly instrumented.

        Args:
            application (FastAPI): The FastAPI application to instrument.

        Raises:
            GrantonTracerError: If the application cannot be instrumented.
        """

        if FastAPIInstrumentor().is_instrumented_by_opentelemetry:
            FastAPIInstrumentor.instrument_app(application)
        else:
            raise GrantonTracerError(f'Application is not instrumented')

    def _setup_tracing(self):
        """Sets up application tracing with Azure Monitor and OpenTelemetry.

        This method attempts to configure tracing with Azure Monitor using either the provided connection string or one
        found in the environment variables. It then applies OpenTelemetry instrumentation to enable tracing.
        """

        if not self.app_insight_connection_string:
            self.app_insight_connection_string = os.getenv('APP_INSIGHT_CONNECTION_STRING')

        if self.app_insight_connection_string:
            try:
                self._configure_azure_monitor_trace_exporter(self.app_insight_connection_string)
                FastAPIInstrumentor().instrument()
                RequestsInstrumentor().instrument()  # Instrumentation of all regular requests
                HTTPXClientInstrumentor().instrument()  # Instrumentation of HTTPX requests
                AioHttpClientInstrumentor().instrument()  # Instrumentation of Open AI
            except Exception as e:
                raise GrantonTracerError(f'Cannot set up tracing instrumentation: {e}')
