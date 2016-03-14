..  _overview-chapter:

======================================
Overview of Data Collection Software
======================================

The Data Collection software at the GSECARS X-ray Microprobe is provides
easy collection of simple line scans, XRF maps, XAFS spectra, and XRD
images for non-expert users while also allowing setting up automated
sequences of commands and, if needed, complex scripting.  The software is
built on top of the Epics control system, providing simple and robust
access to the underlying detectors, motorized stages, monochromators, and
so on.  While these components can be used for many types of general data
acquisition, the interface and collection of available tasks has been
customized for the GSECARS X-ray Microprobe.  This chapter describes some
of the details of the data collection system.

The main data collection program (the *Epics Scans* GUI) provides intuitive
Graphical forms for defining and executing essentially all the beamline
controls and data acquisition tasks needed to collect X-ray microprobe
data.  It also allows the composition of a *Macro Scipt* , to run a
sequence of pre-defined data collection procedures.  These procedures are
custom-built for the beamline, and can be altered dynamically to provide
new or customized data collection tasks.

Client-Server + Database Model
===================================

The Epics Scan software runs as a *Client-Server* system.  There is an
underlying *Scan Server Process* running on a remote machine that is really
collecting most of the data.  Generally, you won't even see this process,
and will run the Epics Scan Graphical User Interface which is a *Client*
that does little more than preparing scan data to be executed by the
*Server*.  This separation of tasks has many advantages, including the
ability to interrupt and control scans from other clients.  We're not doing
that yet, but it will help us support remote access. 

The Client-Server Model requires a way to communicate information between
the two processes.  In addition, the Server needs to hold information about
the beamline detectors, stages, and som on, as well as scan parameters and
details about what data is being collected, has been collected, and will be
collected.  A relational databases system can fill both of these needs, and
we use a PostgresQL database to hold all such information, including a fair
amount of *metadata* about the beamline configuration.



Server Processes
=======================

The server runs on a Linux machine, and there are 3 processes needed for
the system to work.  We are currently using the `epics` account on
`millenia` for all data collection tasks.

The first process used for data collection is the PostgresQL database
engine, which should work without problem.  Currently, we're using one
database per run cycle, named `escan2016_1`, and so on.  This gets backed
up everyday to the `dbsave` directory.  As the analysis tools evolve, we
expect to use the data in this database for analysis tools as well, and may
create a new database per experiment.  For direct SQL access this database,
use::

    ~> psql -W escan2016_1
    Password:
    psql (9.4.6)
    Type "help" for help.
    escan2016_1=# select keyname, value from info order by keyname;
              keyname           |                      value
    ----------------------------+--------------------------------------------------
     command_error              |
     command_running            | 0
     command_status             |
     current_command            | pos_scan('ZnFTCtop_spot4c', 'S_XANES', number=3)
     current_command_id         | 20930


The second process used for data collection is the Scan Server itself.  If
something goes wrong, this may need to be restarted.  Use::

    ~> start_process scan_server

to connect to the *procServ* server process. Use `Ctrl-C` to restart this
process.  The log file for this process, containing all status messages, is
written to `logs/scan_server.log`.  The scan server process should also
respond to executing the :func:`server_restart` command from the Scan macro
window.

Finally, Fast XRF maps (slew scans) are currently collected using a
separate process.  Though this rarely needs attention, it is also running
as a `procServ` server, and can be accesed with::

    ~> start_process fast_map

Its log file is in `logs/fast_map.log`.
