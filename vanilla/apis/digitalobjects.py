# -*- coding: utf-8 -*-

"""
B2SAFE HTTP REST API endpoints.
"""

from __future__ import absolute_import

import os
# from commons import htmlcodes as hcodes
from commons.logs import get_logger
from ..base import ExtendedApiResource
from ..services.irods.client import IrodsException
from ..services.uploader import Uploader
from ..services.irods.translations import Irods2Graph
from .. import decorators as decorate
from ...auth import authentication
from ...confs import config

logger = get_logger(__name__)


###############################
# Classes

class EntitiesEndpoint(Uploader, ExtendedApiResource):

    @authentication.authorization_required
    @decorate.apimethod
    @decorate.catch_error(exception=IrodsException, exception_label='iRODS')
    def get(self, doid=None, eid=None):
        """
        Download file from eid
        """
        if doid is None and eid is None:
            return self.method_not_allowed()

        raise NotImplementedError("Yet to do")

    #     graph = self.global_get_service('neo4j')

    #     # Getting the list
    #     if uuid is None:
    #         data = self.formatJsonResponse(graph.DigitalEntity.nodes.all())
    #         return self.force_response(data)

    #     # # If trying to use a path as file
    #     # elif name[-1] == '/':
    #     #     return self.force_response(
    #     #         errors={'dataobject': 'No dataobject/file requested'})

    #     # Do irods things
    #     icom = self.global_get_service('irods')
    #     user = icom.get_current_user()

    #     # Get filename and ipath from uuid using the graph
    #     try:
    #         dataobj_node = graph.DigitalEntity.nodes.get(id=uuid)
    #     except graph.DigitalEntity.DoesNotExist:
    #         return self.force_response(errors={uuid: 'Not found.'})
    #     collection_node = dataobj_node.belonging.all().pop()

    #     # irods paths
    #     ipath = icom.get_irods_path(
    #         collection_node.path, dataobj_node.filename)

    #     abs_file = self.absolute_upload_file(dataobj_node.filename, user)
    #     # Make sure you remove any cached version to get a fresh obj
    #     try:
    #         os.remove(abs_file)
    #     except:
    #         pass

    #     # Execute icommand (transfer data to cache)
    #     icom.open(ipath, abs_file)

    #     # Download the file from local fs
    #     filecontent = super().download(
    #         dataobj_node.filename, subfolder=user, get=True)

    #     # Remove local file
    #     os.remove(abs_file)

    #     # Stream file content
    #     return filecontent

    @authentication.authorization_required
    # @decorate.add_endpoint_parameter('collection')
    @decorate.add_endpoint_parameter('force', ptype=bool, default=False)
    @decorate.apimethod
    @decorate.catch_error(exception=IrodsException, exception_label='iRODS')
    def post(self):
        """
        Handle file upload
        http --form POST localhost:8080/api/dataobjects \
            file@docker-compose.test.yml

        Test with:
    http --form POST $SERVER/api/entities file@/tmp/gettoken force=True "$AUTH"
        """

###########################
## This should become the base of each authenticated request...
        # Note: graph holds the authenticated accounts in our architecture
        graph = self.global_get_service('neo4j')
        icom = self.global_get_service('irods')
        graphuser = self.get_current_user()
        irodsuser = icom.translate_graph_user(graph, graphuser)
        user = irodsuser.username
        print("TEST", user)
## This should become the base of each authenticated request...
###########################

        # Original upload
        response = super(EntitiesEndpoint, self).upload(subfolder=user)

        # If response is success, save inside the database
        key_file = 'filename'
        filename = None

        content, errors, status = \
            self.get_content_from_response(response, get_all=True)

        if isinstance(content, dict) and key_file in content:
            filename = content[key_file]
            abs_file = self.absolute_upload_file(filename, user)
            logger.info("File is '%s'" % abs_file)

            ############################
            # Move file inside irods

            # ##HANDLING PATH
            # The home dir for the current user
            # Where to put the file in irods
            ipath = icom.get_irods_path(
                self._args.get('collection'), filename)

            try:
                iout = icom.save(
                    abs_file, destination=ipath, force=self._args.get('force'))
                logger.info("irods call %s", iout)
            finally:
                # Remove local cache in any case
                os.remove(abs_file)

            # Call internally the POST method for DO endpoint
            doid = DigitalObjectsEndpoint()._post(graph, icom, graphuser)
            eid = None
            print("IDS", doid, eid)
            # Return link to the file /api/digitalobjects/DOID/entities/EID

        # Reply to user
        content = "TO BE COMPLETED"
        return self.force_response(content, errors=errors, code=status)

    @authentication.authorization_required(roles=config.ROLE_INTERNAL)
    @decorate.apimethod
    @decorate.catch_error(exception=IrodsException, exception_label='iRODS')
    def delete(self, doid=None, mid=None):
        """ Remove an object """

        if doid is not None:
            raise NotImplementedError("Don't have digital objects yet...")

    #     # Get the dataobject from the graph
    #     graph = self.global_get_service('neo4j')
    #     dataobj_node = graph.DigitalEntity.nodes.get(id=uuid)
    #     collection_node = dataobj_node.belonging.all().pop()

    #     icom = self.global_get_service('irods')
    #     ipath = icom.get_irods_path(
    #         collection_node.path, dataobj_node.filename)

    #     # # Remove from graph:
    #     # # Delete with neomodel the dataobject
    #     # try:
    #     #     dataobj_node.delete()
    #     # except graph.DigitalEntity.DoesNotExist:
    #     #     return self.force_response(errors={uuid: 'Not found.'})

    #     # # Delete collection if not linked to any dataobject anymore?
    #     # if len(collection_node.belongs.all()) < 1:
    #     #     collection_node.delete()

    #     # Remove from irods
    #     icom.remove(ipath)
    #     logger.info("Removed %s", ipath)

    #     return self.force_response({'deleted': ipath})


class DigitalObjectsEndpoint(ExtendedApiResource):

    @authentication.authorization_required
    @decorate.apimethod
    @decorate.catch_error(exception=IrodsException, exception_label='iRODS')
    def get(self, doid=None):
        """
        Get object from ID
        """

        return "TO DO!"

    @authentication.authorization_required
    # @decorate.add_endpoint_parameter('user')
    # @decorate.add_endpoint_parameter('force', ptype=bool, default=False)
    @decorate.apimethod
    @decorate.catch_error(exception=IrodsException, exception_label='iRODS')
    def post(self):
        """
        Create an id for the digital object
        """

        user = self._args.get('user', None)
        if user is not None:
            userobj = None
            raise NotImplementedError("Must recover the graph obj from user")
        else:
            userobj = self.get_current_user()

        graph = self.global_get_service('neo4j')
        icom = self.global_get_service('irods')
        uuid = self._post(graph, icom, userobj)

        # Reply to user
        return self.force_response(uuid)  # , errors=errors, code=status)

    def _post(self, graph, icom, user):

## TO BE FIXED

        # Make DOID

        # Create the dataobject...

        # If location, do some collection/aggregations/resource/zone things
        # and connect them

        # Link object to user

        """
            # translate = DataObjectToGraph(graph=graph, icom=icom)
            # uuid = translate.ifile2nodes(
            #     ipath, service_user=self.global_get('custom_auth')._user)
        """

        return 'TO DO'

    # @authentication.authorization_required
    # @decorate.apimethod
    # @decorate.catch_error(exception=IrodsException, exception_label='iRODS')
    # def delete(self, uuid):
    #     """ Remove DO """


class CollectionEndpoint(ExtendedApiResource):
    """
    This endpoint does not exist anymore.
    It is referred as DigitalObject or Aggregation,
    which are graph Nodes but we do not have a dedicated endpoint
    """

    pass

#     @authentication.authorization_required
#     @decorate.apimethod
#     @decorate.catch_error(exception=IrodsException, exception_label='iRODS')
#     def get(self, uuid=None):
#         """
#         Return list of elements inside a collection.
#         If uuid is added, get the single element.
#         """

#         graph = self.global_get_service('neo4j')

#     ##########
# ## // TO FIX!!
# # List collections and dataobjects only linked to current user :)

#         # auth = self.global_get('custom_auth')
#         # graph_user = auth.get_user_object(payload=auth._payload)
#         # # get the irods_user connected to graph_user
#         # icom = self.global_get_service('irods', user=FIND_THE_USER)
#     ##########

#         content = []

#         # Get ALL elements
#         if uuid is None:
#             content = graph.Collection.nodes.all()
#         # Get SINGLE element
#         else:
#             try:
#                 content.append(graph.Collection.nodes.get(id=uuid))
#             except graph.Collection.DoesNotExist:
#                 return self.force_response(errors={uuid: 'Not found.'})

#         # Build jsonapi.org compliant response
#         data = self.formatJsonResponse(content)
#         return self.force_response(data)

# ###############
# ## // TO DO:
# # The one above is such a standard 'get' method that
# # we could make it general for the graphdb use case
# ###############

#     @authentication.authorization_required
#     @decorate.add_endpoint_parameter('collection', required=True)
#     @decorate.add_endpoint_parameter('force', ptype=bool, default=False)
#     @decorate.apimethod
#     @decorate.catch_error(exception=IrodsException, exception_label='iRODS')
#     def post(self):
#         """ Create one collection/directory """

#         icom = self.global_get_service('irods')
#         collection_input = self._args.get('collection')
#         ipath = icom.create_empty(
#             collection_input,
#             directory=True, ignore_existing=self._args.get('force'))
#         logger.info("Created irods collection: %s", ipath)

#         # Save inside the graph and give back the uuid
#         translate = DataObjectToGraph(
#             icom=icom, graph=self.global_get_service('neo4j'))
#         _, collections, zone = translate.split_ipath(ipath, with_file=False)
#         node = translate.recursive_collection2node(
#             collections, current_zone=zone)

#         return self.force_response(
#             {'id': node.id, 'collection': ipath},
#             code=hcodes.HTTP_OK_CREATED)

#     @authentication.authorization_required
#     @decorate.add_endpoint_parameter('collection', required=False)
#     @decorate.apimethod
#     @decorate.catch_error(exception=IrodsException, exception_label='iRODS')
#     def delete(self, uuid):
#         """ Remove an object """

#         # Get the dataobject from the graph
#         graph = self.global_get_service('neo4j')
#         node = None
#         try:
#             node = graph.Collection.nodes.get(id=uuid)
#         except graph.Collection.DoesNotExist:
#             return self.force_response(errors={uuid: 'Not found.'})

#         icom = self.global_get_service('irods')
#         ipath = icom.handle_collection_path(node.path)

#         # Remove from graph:
#         node.delete()
#         # Remove from irods
#         icom.remove(ipath, recursive=True)
#         logger.info("Removed collection %s", ipath)

#         return self.force_response({'deleted': ipath})

