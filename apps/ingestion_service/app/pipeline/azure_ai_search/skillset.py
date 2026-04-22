"""Builders to create Azure Search skillsets for EduWeaver."""

from __future__ import annotations

import logging

from azure.search.documents.indexes.models import (
    AIServicesAccountKey,
    AzureOpenAIEmbeddingSkill,
    DocumentIntelligenceLayoutSkill,
    DocumentIntelligenceLayoutSkillChunkingProperties,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SearchIndexerSkillset,
)

from apps.ingestion_service.app.config.settings import (
    AIModelSettings,
    DocumentIntelligenceSettings,
    SkillsetSettings,
)
from apps.ingestion_service.app.indexing.vector_indexer import SearchIndexerService

logger = logging.getLogger(__name__)


class SkillsetService:
    """Manage creation of the Azure Search skillset used in our RAG pipeline."""

    def __init__(self) -> None:
        self._client = SearchIndexerService().get_client()
        self._name = SkillsetSettings.get_name()
        self._description = SkillsetSettings.get_description()

    def create_or_update_skillset(self) -> str:
        skillset = self._build_skillset()
        self._client.create_or_update_skillset(skillset)
        logger.info(
            "Skillset '%s' created or updated with %d skills",
            skillset.name,
            len(skillset.skills),
        )
        return skillset.name

    def _build_skillset(self) -> SearchIndexerSkillset:
        return SearchIndexerSkillset(
            name=self._name,
            description=self._description,
            skills=[
                self._build_layout_skill(),
                self._build_embedding_skill(),
            ],
            cognitive_services_account=AIServicesAccountKey(
                key=DocumentIntelligenceSettings.get_key(),
                subdomain_url=DocumentIntelligenceSettings.get_endpoint(),
            ),
        )

    def _build_layout_skill(self) -> DocumentIntelligenceLayoutSkill:
        return DocumentIntelligenceLayoutSkill(
            name="layout-skill",
            context="/document",
            output_mode="oneToMany",
            output_format="text",
            extraction_options=["images", "locationMetadata"],
            chunking_properties=DocumentIntelligenceLayoutSkillChunkingProperties(
                unit="characters",
                maximum_length=SkillsetSettings.get_chunk_max_length(),
                overlap_length=SkillsetSettings.get_chunk_overlap_length(),
            ),
            inputs=[
                InputFieldMappingEntry(
                    name="file_data",
                    source="/document/file_data",
                )
            ],
            outputs=[
                OutputFieldMappingEntry(
                    name="text_sections", target_name="text_sections"
                ),
                OutputFieldMappingEntry(
                    name="normalized_images", target_name="normalized_images"
                ),
            ],
        )

    def _build_embedding_skill(self) -> AzureOpenAIEmbeddingSkill:
        return AzureOpenAIEmbeddingSkill(
            name="embedding-skill",
            context="/document/text_sections/*",
            resource_url=AIModelSettings.get_openai_endpoint(),
            deployment_name=AIModelSettings.get_embedding_deployment_name(),
            api_key=AIModelSettings.get_api_key(),
            inputs=[
                InputFieldMappingEntry(
                    name="text", source="/document/text_sections/*/content"
                )
            ],
            outputs=[
                OutputFieldMappingEntry(name="vector", target_name="content_embedding")
            ],
        )
